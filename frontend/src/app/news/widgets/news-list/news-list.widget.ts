import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NewsPost } from '../../news-post/news-post.model';
import { Organization } from 'src/app/organization/organization.model';

@Component({
  selector: 'news-list',
  templateUrl: './news-list.widget.html',
  styleUrls: ['./news-list.widget.css']
})
export class NewsList {
  /** The event for the event card to display */
  @Input() postsPerDay: [string, NewsPost[]][] = [];

  /** The organization associated with the Event List for the Organization Details Page */
  @Input() organization: String | null = null;

  /** Store the selected Event */
  @Input() selectedPost: NewsPost | null = null;

  /** Whether or not to disable the links on the page */
  @Input() disableLinks: boolean = false;

  @Input() showHeader: boolean = false;

  /** Whether or not to disable the event creation button */
  @Input() showCreateButton: boolean = false;

  /** Whether or not the event list should be full width */
  @Input() fullWidth: boolean = false;

  /** Event binding for the card's on click action */
  @Output() cardClicked: EventEmitter<NewsPost> = new EventEmitter();

  /** Constructs the widget */
  constructor() {}
}
