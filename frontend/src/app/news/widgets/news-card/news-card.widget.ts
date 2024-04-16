import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Event } from 'src/app/event/event.model';
import { NewsPost } from '../../news-post/news-post.model';

@Component({
  selector: 'news-card',
  templateUrl: './news-card.widget.html',
  styleUrls: ['./news-card.widget.css']
})
export class NewsCard {
  /** The post for the news card to display */
  @Input() post!: NewsPost;

  /** Whether to disable the tile link or not */
  @Input() disableLink!: Boolean;

  /** Whether or not the current card is selected */
  @Input() selected: Boolean = false;

  /** Provides the event to a handler for the on click action */
  @Output() clicked = new EventEmitter<NewsPost>();

  constructor() {}

  /** Handler for when the news card is pressed */
  cardClicked() {
    if (this.disableLink) {
      this.clicked.emit(this.post);
    }
  }
}
