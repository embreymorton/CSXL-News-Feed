import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { RxNewsPost } from 'src/app/news/rx-news-post';
import { NewsPost } from 'src/app/news/news-post.model';
import { Paginated, PaginationParams } from 'src/app/pagination';

@Injectable({ providedIn: 'root' })
export class AdminNewsService {
  private newsPosts: RxNewsPost = new RxNewsPost();
  public newPosts$: Observable<NewsPost[]> = this.newsPosts.value$;

  constructor(protected http: HttpClient) {}

  list(params: PaginationParams) {
    let paramStrings = {
      page: params.page.toString(),
      page_size: params.page_size.toString(),
      order_by: params.order_by,
      filter: params.filter
    };
    let query = new URLSearchParams(paramStrings);
    return this.http.get<Paginated<NewsPost>>(
      '/api/admin/news?' + query.toString()
    );
  }

  /** Returns a list of all published NewsPosts
   * @returns {Observable<NewsPost[]>}
   */
  list_published(): void {
    this.http
      .get<NewsPost[]>('/api/news/published')
      .subscribe((newsPosts) => this.newsPosts.set(newsPosts));
  }

  /** Returns a list of all incoming NewsPosts
   * @returns {Observable<NewsPost[]>}
   */
  list_incoming(): void {
    this.http
      .get<NewsPost[]>('/api/news/incoming')
      .subscribe((newsPosts) => this.newsPosts.set(newsPosts));
  }

  /** Returns a list of all archived NewsPosts
   * @returns {Observable<NewsPost[]>}
   */
  list_archived(): void {
    this.http
      .get<NewsPost[]>('/api/news/archived')
      .subscribe((newsPosts) => this.newsPosts.set(newsPosts));
  }

  /** Creates a newsPost
   * @param newNewsPost: NewsPost object that you want to add to the database
   * @returns {Observable<NewsPost>}
   */
  createNewsPost(newNewsPost: NewsPost): Observable<NewsPost> {
    return this.http
      .post<NewsPost>('/api/news', newNewsPost)
      .pipe(tap((newsPost) => this.newsPosts.pushNewsPost(newsPost)));
  }

  /** Publishes a newsPost
   * @param newsPost: NewsPost object that you want to publish to the news feed
   * @returns {Observable<NewsPost>}
   */
  publishNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    newsPost.state = 'published';
    return this.http
      .put<NewsPost>('/api/news', newsPost)
      .pipe(tap((newsPost) => this.newsPosts.removeNewsPost(newsPost)));
  }

  /** Archives a newsPost
   * @param newsPost: NewsPost object that you want to save as an archived post
   * @returns {Observable<NewsPost>}
   */
  archiveNewsPost(newsPost: NewsPost): Observable<NewsPost> {
    newsPost.state = 'archived';
    return this.http
      .put<NewsPost>('/api/news', newsPost)
      .pipe(tap((newsPost) => this.newsPosts.removeNewsPost(newsPost)));
  }

  /** Deletes a newsPost
   * @param newsPostToRemove: NewsPost object to delete
   * @returns {Observable<NewsPost>}
   */
  deleteNewsPost(newsPostToRemove: NewsPost): Observable<NewsPost> {
    return this.http
      .delete<NewsPost>(`/api/news/${newsPostToRemove.slug}`)
      .pipe(
        tap((_) => {
          this.newsPosts.removeNewsPost(newsPostToRemove);
        })
      );
  }
}
