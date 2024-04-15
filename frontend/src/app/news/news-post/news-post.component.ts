import { Component } from '@angular/core';

@Component({
  selector: 'app-news-post',
  templateUrl: './news-post.component.html'
})
export class NewsPostComponent {
  public static Route = {
    path: 'post',
    component: NewsPostComponent
  };
}
