import { Component } from '@angular/core';
import { NewsPostService } from '../news-post.service';
import { NewsPost } from '../news-post/news-post.model';

@Component({
  selector: 'app-news-feed',
  templateUrl: './news-feed.component.html',
  styleUrls: ['./news-feed.component.css']
})
export class NewsFeedComponent {
  public static Route = {
    path: 'news',
    title: 'CSXL News Feed',
    component: NewsFeedComponent
  };

  constructor(public newsService: NewsPostService) {}

  postList: NewsPost[] = this.newsService.getNewsPosts();
}
