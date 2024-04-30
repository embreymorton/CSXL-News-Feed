import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Event } from 'src/app/event/event.model';
import { NewsPost } from '../../news-post.model';
import { Router } from '@angular/router';
import { AdminNewsService } from 'src/app/admin/news/admin-news.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrls: ['./news-card.widget.css']
})
export class NewsCard {
  /** The post for the news card to display */
  @Input() post!: NewsPost;

  public newsPosts$: Observable<NewsPost[]>;

  /** Whether to disable the tile link or not */
  @Input() disableLink!: Boolean;

  /** Whether or not the current card is selected */
  @Input() selected: Boolean = false;

  /** Provides the event to a handler for the on click action */
  @Output() clicked = new EventEmitter<NewsPost>();

  constructor(
    private router: Router,
    private adminNewsService: AdminNewsService
  ) {
    this.newsPosts$ = adminNewsService.newPosts$;
    adminNewsService.list_published();
  }

  /** Handler for when the news card is pressed */
  cardClicked() {
    if (this.disableLink) {
      this.clicked.emit(this.post);
    }
  }

  editPost(newsPost: NewsPost): void {
    const editUrl = `/news/${newsPost.slug}/edit`;
    try {
      this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
        this.router.navigate([editUrl]);
      });
    } catch (error) {
      console.error('Navigation failed:', error);
    }
  }
}
