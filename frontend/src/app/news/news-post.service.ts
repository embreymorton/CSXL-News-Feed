import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs';
import { NewsPost } from './news-post/news-post.model';

@Injectable({
  providedIn: 'root'
})
export class NewsPostService {
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar
  ) {}

  /** Returns all newsPost entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<NewsPost[]>}
   */
  getNewsPosts() {
    const post1: NewsPost = {
      id: 1,
      headline: 'News Feed Component in the Works',
      synopsis: 'Team B1 is Grinding',
      main_story:
        'Team B1 has been grinding during Sprint Zero to create a news feed component for COMP 423. The formatting could use some work.',
      author: 'Author: Team B1',
      organization: 'Organization',
      state: 'string',
      slug: 'string',
      image_url: 'string',
      publish_date: 'Publish Date: April 2nd',
      modification_date: 'Modification Date: April 2nd'
    };

    let dummy_list: NewsPost[] = [];
    dummy_list.push(post1);
    dummy_list.push(post1);
    dummy_list.push(post1);
    dummy_list.push(post1);
    dummy_list.push(post1);
    dummy_list.push(post1);

    return dummy_list;

    //return this.http.get<NewsPost[]>('/api/news_post');
  }

  /** Returns the newsPost object from the backend database table using the backend HTTP get request.
   * @param slug: String representing the newsPost slug
   * @returns {Observable<NewsPost>}
   */
  getNewsPost(slug: string): Observable<NewsPost> {
    return this.http.get<NewsPost>('/api/news_post/' + slug);
  }

  /** Returns the new newsPost object from the backend database table using the backend HTTP post request.
   * @param newsPost: NewsPostSummary representing the new newsPost
   * @returns {Observable<NewsPost>}
   */
  createNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.post<NewsPost>('/api/news_post', newsPost);
  }

  /** Returns the updated newsPost object from the backend database table using the backend HTTP put request.
   * @param newsPost: NewsPostSummary representing the updated newsPost
   * @returns {Observable<NewsPost>}
   */
  updateNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    return this.http.put<NewsPost>('/api/organizations', newsPost);
  }
}
