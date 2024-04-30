import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, Subscription, map } from 'rxjs';
import { NewsPost, NewsPostJson, parsePostJson } from './news-post.model';
import { DatePipe } from '@angular/common';
import { EventPaginationParams, PaginatedEvent } from '../pagination';
import { Profile, ProfileService } from '../profile/profile.service';
import { EventJson, parseEventJson } from '../event/event.model';
import { Organization } from '../organization/organization.model';

@Injectable({
  providedIn: 'root'
})
export class NewsPostService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar,
    public datePipe: DatePipe,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  /** Returns all newsPost entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getNewsPosts(): Observable<NewsPost[]> {
    return this.http.get<NewsPost[]>('/api/news');
  }

  /** Returns all draft entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getDrafts(): Observable<NewsPost[]> {
    return this.http.get<NewsPost[]>('/api/news/drafts');
  }

  /** Returns all published newsPost entries by an organization using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getNewsPostsByOrganization(slug: String): Observable<NewsPost[]> {
    return this.http.get<NewsPost[]>('/api/news/organization/' + slug);
  }

  /** Returns all published newsPost entries by a user using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getNewsPostsByAuthor(id: number): Observable<NewsPost[]> {
    return this.http.get<NewsPost[]>('/api/news/author/' + id);
  }

  /** Returns all draft newsPost entries by a user using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getDraftsByAuthor(id: number): Observable<NewsPost[]> {
    return this.http.get<NewsPost[]>('/api/news/author/drafts/' + id);
  }

  /** Returns the newsPost object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the newsPost slug
   * @returns {Observable<NewsPost>}
   */
  getNewsPost(slug: string): Observable<NewsPost> {
    return this.http.get<NewsPost>('/api/news/' + slug);
  }

  /** Returns the new newsPost object from the backend database table using the backend HTTP post request.
   * @param newsPost: NewsPostSummary representing the new newsPost
   * @returns {Observable<NewsPost>}
   */
  createNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.post<NewsPost>('/api/news', newsPost);
  }

  /** Returns the updated newsPost object from the backend database table using the backend HTTP put request.
   * @param newsPost: NewsPostSummary representing the updated newsPost
   * @returns {Observable<NewsPost>}
   */
  updateNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.put<NewsPost>('/api/news', newsPost);
  }

  deleteNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.delete<NewsPost>('/api/news/' + newsPost.slug);
  }

  publishNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    newsPost.state = 'published';
    return this.http.put<NewsPost>('/api/news', newsPost);
  }

  groupPostsByDate(
    posts: NewsPost[],
    query: string = ''
  ): [string, NewsPost[]][] {
    // Initialize an empty map
    let groups: Map<string, NewsPost[]> = new Map();

    // Transform the list of events based on the event filter pipe and query
    posts.forEach((post) => {
      // Find the date to group by
      let dateString =
        this.datePipe.transform(post.time, 'EEEE, MMMM d, y') ?? '';
      // Add the event
      let newPostsList = groups.get(dateString) ?? [];
      newPostsList.push(post);
      groups.set(dateString, newPostsList);
    });

    // Return the groups
    return [...groups.entries()];
  }

  list(params: EventPaginationParams) {
    let paramStrings = {
      order_by: params.order_by,
      ascending: params.ascending,
      filter: params.filter,
      range_start: params.range_start,
      range_end: params.range_end
    };
    let query = new URLSearchParams(paramStrings);
    if (this.profile) {
      // this.http
      //   .get<PaginatedEvent<NewsPostJson>>(
      //     'api/news_posts/paginate?' + query.toString()
      //   )
      //   .subscribe((values) => console.log(values));
      return this.http
        .get<PaginatedEvent<NewsPostJson>>(
          'api/news/paginate?' + query.toString()
        )
        .pipe(
          map((paginated) => ({
            ...paginated,
            items: paginated.items.map(parsePostJson)
          }))
        );
    } else {
      // if a user isn't logged in, return the normal endpoint without registration statuses
      return this.http
        .get<PaginatedEvent<NewsPostJson>>(
          'api/news/paginate/unauthenticated?' + query.toString()
        )
        .pipe(
          map((paginated) => ({
            ...paginated,
            items: paginated.items.map(parsePostJson)
          }))
        );
    }
  }
}
