import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Profile } from 'src/app/models.module';
import { NewsPost } from './news-post.model';
import { NewsPostService } from '../news-post.service';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { NewsPostDetailResolver } from '../news.resolver';

/** Injects the posts's headline to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['post']?.headline ?? 'Post Not Found';
};

@Component({
  selector: 'app-news-post',
  templateUrl: './news-post.component.html',
  styleUrls: ['./news-post.component.css']
})
export class NewsPostComponent {
  public static Route = {
    title: 'News',
    path: 'news/:slug',
    component: NewsPostComponent,
    resolve: {
      profile: profileResolver,
      post: NewsPostDetailResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: NewsPostComponent
      }
    ]
  };

  public profile: Profile;

  public newsPost: NewsPost;

  constructor(
    private route: ActivatedRoute,
    protected newsService: NewsPostService
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      post: NewsPost;
    };
    this.profile = data.profile;
    this.newsPost = data.post;
  }
}
