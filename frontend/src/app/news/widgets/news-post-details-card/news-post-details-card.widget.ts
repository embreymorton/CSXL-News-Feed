import { Component, Input, OnDestroy, OnInit } from '@angular/core';

import { NewsPost } from '../../news-post/news-post.model';

@Component({
  selector: 'news-post-details-card',
  templateUrl: './news-post-details-card.widget.html',
  styleUrls: ['./news-post-details-card.widget.css']
})
export class NewsPostDetailsCard {
  @Input() news_post?: NewsPost;

  constructor() {}
}
