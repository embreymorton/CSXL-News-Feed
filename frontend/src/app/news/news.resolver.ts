import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { NewsPost } from './news-post.model';
import { NewsPostService } from './news-post.service';
import { catchError, map, of } from 'rxjs';

/** This resolver injects the list of posts into the post component. */
export const newsPostResolver: ResolveFn<NewsPost[] | undefined> = (
  route,
  state
) => {
  return inject(NewsPostService).getNewsPosts();
};

/** This resolver injects an post into the post detail component. */
export const NewsPostDetailResolver: ResolveFn<NewsPost | undefined> = (
  route,
  state
) => {
  // If the post is new, return a blank one
  if (route.paramMap.get('slug')! == 'new') {
    return {
      id: 0,
      headline: '',
      synopsis: '',
      main_story: '',
      author_id: null,
      author: null,
      organization_id: null,
      organization: null,
      state: '',
      slug: '',
      image_url: '',
      time: new Date(),
      modification_date: new Date()
    };
  }

  // Otherwise, return the news post.
  // If there is an error, return undefined
  return inject(NewsPostService)
    .getNewsPost(route.paramMap.get('slug')!)
    .pipe(
      catchError((error) => {
        console.log(error);
        return of(undefined);
      })
    );
};
