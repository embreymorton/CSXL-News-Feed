/* The RxNewsPost object is used to ensure proper updating and
 retrieval of the list of all NewsPosts in the database.
*/

import { RxObject } from '../rx-object';
import { NewsPost } from './news-post.model';

export class RxNewsPost extends RxObject<NewsPost[]> {
  pushNewsPost(newsPost: NewsPost): void {
    this.value.push(newsPost);
    this.notify();
  }

  updateNewsPost(newsPost: NewsPost): void {
    this.value = this.value.map((n) => {
      return n.id !== newsPost.id ? n : newsPost;
    });
    this.notify();
  }

  removeNewsPost(newsPostToRemove: NewsPost): void {
    this.value = this.value.filter(
      (newsPost) => newsPostToRemove.slug !== newsPost.slug
    );
    this.notify();
  }
}
