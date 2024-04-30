import {
  Component,
  HostListener,
  OnDestroy,
  OnInit,
  inject
} from '@angular/core';
import { NewsPostService } from '../news-post.service';
import { NewsPost } from '../news-post.model';
import { PaginatedEvent } from 'src/app/pagination';
import {
  Subject,
  Subscription,
  debounceTime,
  distinctUntilChanged,
  filter,
  tap
} from 'rxjs';
import { Profile } from 'src/app/models.module';
import { ActivatedRoute, ActivationEnd, Params, Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-news-feed',
  templateUrl: './news-feed.component.html',
  styleUrls: ['./news-feed.component.css']
})
export class NewsFeedComponent implements OnInit, OnDestroy {
  public page: PaginatedEvent<NewsPost>;
  public startDate = new Date(new Date().setDate(new Date().getDate() - 7));
  public endDate = new Date();
  public today: boolean = true;

  //postList: NewsPost[] = this.newsService.getNewsPosts();

  private static EventPaginationParams = {
    order_by: 'time',
    ascending: 'false',
    filter: '',
    range_start: new Date(
      new Date().setDate(new Date().getDate() - 7)
    ).toLocaleString('en-GB'),
    range_end: new Date().toLocaleString('en-GB')
  };

  public static Route = {
    path: 'news',
    title: 'News Feed',
    component: NewsFeedComponent,
    canActivate: [],
    resolve: {
      profile: profileResolver,
      page: () =>
        inject(NewsPostService).list(NewsFeedComponent.EventPaginationParams)
    }
  };

  /** Store the content of the search bar */
  public searchBarQuery = '';

  /** Store a map of days to a list of events for that day */
  public postsPerDay: [string, NewsPost[]][];

  /** Store the selected Post */
  public selectedPost: NewsPost | null = null;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** Stores the width of the window. */
  public innerWidth: any;

  /** Search bar query string */
  public query: string = '';

  public searchUpdate = new Subject<string>();

  private routeSubscription!: Subscription;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public datePipe: DatePipe,
    public newsService: NewsPostService
  ) {
    // Initialize data from resolvers
    const data = this.route.snapshot.data as {
      profile: Profile;
      page: PaginatedEvent<NewsPost>;
    };
    this.profile = data.profile;
    this.page = data.page;
    this.today =
      this.endDate.setHours(0, 0, 0, 0) == new Date().setHours(0, 0, 0, 0);

    // Group events by their dates
    this.postsPerDay = newsService.groupPostsByDate(this.page.items);

    // Initialize the initially selected event
    if (data.page.items.length > 0) {
      this.selectedPost = this.page.items[0];
    }

    this.searchUpdate
      .pipe(
        filter((search: string) => search.length > 2 || search.length == 0),
        debounceTime(500),
        distinctUntilChanged()
      )
      .subscribe((query) => {
        this.onSearchBarQueryChange(query);
      });
  }

  /** Runs when the frontend UI loads */
  ngOnInit() {
    // Keep track of the initial width of the browser window
    this.innerWidth = window.innerWidth;

    // Watch current route's query params
    this.route.queryParams.subscribe((params: Params): void => {
      this.startDate = params['start_date']
        ? new Date(Date.parse(params['start_date']))
        : new Date(new Date().setDate(new Date().getDate() - 7));
      this.endDate = params['end_date']
        ? new Date(Date.parse(params['end_date']))
        : new Date();
    });

    const today = new Date();
    if (this.startDate.getTime() < today.setHours(0, 0, 0, 0)) {
      this.page.params.ascending = 'false';
    }

    let paginationParams = this.page.params;
    paginationParams.range_start = this.startDate.toLocaleString('en-GB');
    paginationParams.range_end = this.endDate.toLocaleString('en-GB');
    this.newsService.list(paginationParams).subscribe((page) => {
      this.postsPerDay = this.newsService.groupPostsByDate(page.items);
    });

    let prevUrl = '';
    this.routeSubscription = this.router.events
      .pipe(
        filter((e) => e instanceof ActivationEnd),
        distinctUntilChanged(() => this.router.url === prevUrl),
        tap(() => (prevUrl = this.router.url))
      )
      .subscribe((_) => {
        this.page.params.ascending = (
          this.startDate.getTime() > today.setHours(0, 0, 0, 0)
        ).toString();
        let paginationParams = this.page.params;
        paginationParams.range_start = this.startDate.toLocaleString('en-GB');
        paginationParams.range_end = this.endDate.toLocaleString('en-GB');
        this.newsService.list(paginationParams).subscribe((page) => {
          this.postsPerDay = this.newsService.groupPostsByDate(page.items);
        });
      });
  }

  ngOnDestroy() {
    this.routeSubscription.unsubscribe();
  }

  /** Handler that runs when the window resizes */
  @HostListener('window:resize', ['$event'])
  onResize(_: UIEvent) {
    // Update the browser window width
    this.innerWidth = window.innerWidth;
  }

  /** Handler that runs when the search bar query changes.
   * @param query: Search bar query to filter the items
   */
  onSearchBarQueryChange(query: string) {
    this.query = query;
    let paginationParams = this.page.params;
    paginationParams.ascending = 'true';
    if (query == '') {
      paginationParams.range_start = this.startDate.toLocaleString('en-GB');
      paginationParams.range_end = this.endDate.toLocaleString('en-GB');
    } else {
      paginationParams.range_start = new Date(
        new Date().setFullYear(new Date().getFullYear() - 100)
      ).toLocaleString('en-GB');
      paginationParams.range_end = new Date(
        new Date().setFullYear(new Date().getFullYear() + 100)
      ).toLocaleString('en-GB');
      paginationParams.filter = this.query;
    }
    this.newsService.list(paginationParams).subscribe((page) => {
      this.postsPerDay = this.newsService.groupPostsByDate(page.items);
      paginationParams.filter = '';
    });
  }

  /** Handler that runs when an event card is clicked.
   * This function selects the event to display on the sidebar.
   * @param event: Event pressed
   */
  onPostCardClicked(post: NewsPost) {
    this.selectedPost = post;
  }

  showPosts(isPrevious: boolean) {
    // Cannot go past today
    if (isPrevious == false && this.today) {
      return;
    }

    this.startDate = isPrevious
      ? new Date(this.startDate.setDate(this.startDate.getDate() - 7))
      : new Date(this.startDate.setDate(this.startDate.getDate() + 7));
    this.endDate = isPrevious
      ? new Date(this.endDate.setDate(this.endDate.getDate() - 7))
      : new Date(this.endDate.setDate(this.endDate.getDate() + 7));
    if (isPrevious === true) {
      this.page.params.ascending = 'false';
    }
    this.today =
      this.endDate.setHours(0, 0, 0, 0) == new Date().setHours(0, 0, 0, 0);

    this.startDate = new Date(this.startDate.setHours(0, 0, 0));
    this.endDate = new Date(this.endDate.setHours(23, 59, 59));

    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        start_date: this.startDate.toISOString(),
        end_date: this.endDate.toISOString()
      },
      queryParamsHandling: 'merge'
    });
  }
}
