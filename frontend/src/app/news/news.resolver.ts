import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import { NewsPost } from './news-post/news-post.model';
import { NewsPostService } from './news-post.service';
import { EventService } from '../event/event.service';
import { Event } from '../event/event.model';
import { catchError, map, of } from 'rxjs';

/** This resolver injects the list of organizations into the organization component. */
export const newsPostResolver: ResolveFn<NewsPost[] | undefined> = (
  route,
  state
) => {
  return inject(NewsPostService).getNewsPosts();
};

/** This resolver injects an organization into the organization detail component. */
export const NewsPostDetailResolver: ResolveFn<NewsPost | undefined> = (
  route,
  state
) => {
  // If the organization is new, return a blank one
  if (route.paramMap.get('slug')! == 'new') {
    return {
      id: 0,
      headline: '',
      synopsis: '',
      main_story: '',
      author: 'String',
      organization: undefined,
      state: '',
      slug: '',
      image_url: '',
      time: new Date(),
      modification_date: new Date()
    };
  }

  // Otherwise, return the organization.
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

/** This resolver injects the events for a given organization into the organization component. */
export const NewsPostEventsResolver: ResolveFn<Event[] | undefined> = (
  route,
  state
) => {
  return inject(EventService).getEventsByOrganization(
    route.paramMap.get('slug')!
  );
};
