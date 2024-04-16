import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, Subscription, map } from 'rxjs';
import {
  NewsPost,
  NewsPostJson,
  parsePostJson
} from './news-post/news-post.model';
import { DatePipe } from '@angular/common';
import { EventPaginationParams, PaginatedEvent } from '../pagination';
import { Profile, ProfileService } from '../profile/profile.service';
import { EventJson, parseEventJson } from '../event/event.model';

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
    // const post1 = {
    //   id: 1,
    //   headline: 'News Feed Component in the Works 1',
    //   synopsis: 'Team B1 is still Grinding',
    //   main_story:
    //     'Team B1 has been grinding during Sprint One to create a news feed component for COMP 423. The formatting is improving.',
    //   author: 'Team B1',
    //   organization: undefined,
    //   state: 'string',
    //   slug: 'string',
    //   image_url: 'string',
    //   publish_date: new Date(), // Today
    //   modification_date: new Date() // Today
    // };

    // const post2 = {
    //   ...post1,
    //   id: 2,
    //   headline: 'News Feed Component in the Works 2',
    //   publish_date: new Date(new Date().setDate(new Date().getDate() - 1)), // Yesterday
    //   modification_date: new Date(new Date().setDate(new Date().getDate() - 1)) // Yesterday
    // };

    // const post3 = {
    //   ...post1,
    //   id: 3,
    //   headline: 'News Feed Component in the Works 3',
    //   publish_date: new Date(new Date().setDate(new Date().getDate() - 2)), // 2 days ago
    //   modification_date: new Date(new Date().setDate(new Date().getDate() - 2)) // 2 days ago
    // };

    // let dummy_list: NewsPost[] = [];
    // dummy_list.push(post1);
    // dummy_list.push(post2);
    // dummy_list.push(post3);
    // dummy_list.push(post3);

    // return dummy_list;

    return this.http.get<NewsPost[]>('/api/news_posts');
  }

  /** Returns the newsPost object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the newsPost slug
   * @returns {Observable<NewsPost>}
   */
  getNewsPost(slug: string): Observable<NewsPost> {
    return this.http.get<NewsPost>('/api/news_posts/' + slug);
  }

  /** Returns the new newsPost object from the backend database table using the backend HTTP post request.
   * @param newsPost: NewsPostSummary representing the new newsPost
   * @returns {Observable<NewsPost>}
   */
  createNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.post<NewsPost>('/api/news_posts', newsPost);
  }

  /** Returns the updated newsPost object from the backend database table using the backend HTTP put request.
   * @param newsPost: NewsPostSummary representing the updated newsPost
   * @returns {Observable<NewsPost>}
   */
  updateNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.put<NewsPost>('/api/news_posts', newsPost);
  }

  deleteNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.delete<NewsPost>('/api/news_posts');
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
      return this.http
        .get<PaginatedEvent<NewsPostJson>>(
          'api/news_posts/paginate?' + query.toString()
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
          'api/news_posts/paginate?' + query.toString()
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
