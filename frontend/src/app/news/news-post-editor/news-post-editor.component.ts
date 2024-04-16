import { Component, inject } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  CanActivateFn,
  Route,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { PermissionService } from 'src/app/permission.service';
import { NewsPost } from '../news-post/news-post.model';
import { NewsPostService } from '../news-post.service';
import { Profile } from 'src/app/profile/profile.service';
import { NewsPostDetailResolver } from '../news.resolver';

const canActivateEditor: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  /** Determine if page is viewable by user based on permissions */

  let slug: string = route.params['slug'];

  if (slug === 'new') {
    return inject(PermissionService).check('newsPost.create', 'newsPost');
  } else {
    return inject(PermissionService).check(
      'newsPost.update',
      `newsPost/${slug}`
    );
  }
};

@Component({
  selector: 'app-news-post-editor',
  templateUrl: './news-post-editor.component.html',
  styleUrls: ['./news-post-editor.component.css']
})
export class NewsPostEditorComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: 'news/:slug/edit',
    component: NewsPostEditorComponent,
    title: 'News Post Editor',
    canActivate: [canActivateEditor],
    resolve: {
      profile: profileResolver,
      newsPost: NewsPostDetailResolver
    }
  };

  /** Store the organization.  */
  public newsPost: NewsPost;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the organization id. */
  newsPost_slug: string = 'new';

  /** Add validators to the form */
  author = new FormControl('', [Validators.required]);
  slug = new FormControl('', [
    Validators.required,
    Validators.pattern('^(?!new$)[a-z0-9-]+$')
  ]);
  logo = new FormControl('', [Validators.required]);
  headline = new FormControl('', [
    Validators.required,
    Validators.maxLength(15000)
  ]);
  synopsis = new FormControl('', [
    Validators.required,
    Validators.maxLength(15000)
  ]);
  main_story = new FormControl('', [Validators.maxLength(200000000000)]);

  /** Organization Editor Form */
  public newsPostForm = this.formBuilder.group({
    headline: this.headline,
    synopsis: this.synopsis,
    main_story: this.main_story,
    author: this.author,
    organization: undefined,
    state: '',
    slug: this.slug,
    image_url: ''
  });

  /** Constructs the organization editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private newsPostService: NewsPostService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      newsPost: NewsPost;
    };
    this.profile = data.profile;
    this.newsPost = data.newsPost;

    /** Get id from the url */
    let newsPost_slug = this.route.snapshot.params['slug'];
    this.newsPost_slug = newsPost_slug;

    if (newsPost_slug != 'new') {
      /** Set organization form data */
      this.newsPostForm.setValue({
        headline: this.newsPost.headline,
        synopsis: this.newsPost.synopsis,
        main_story: this.newsPost.main_story,
        author: this.newsPost.author,
        organization: this.newsPost.organization_id,
        state: this.newsPost.state,
        slug: this.newsPost.slug,
        image_url: this.newsPost.image_url
      });
    }
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.newsPostForm.valid) {
      Object.assign(this.newsPost, this.newsPostForm.value);
      if (this.newsPost_slug == 'new') {
        this.newsPost.id = null;
        this.newsPost.time = new Date();
        this.newsPost.modification_date = new Date();

        console.log(this.newsPost);
        this.newsPostService.createNewsPost(this.newsPost).subscribe({
          next: (newsPost) => this.onSuccess(newsPost),
          error: (err) => this.onError(err)
        });
      } else {
        this.newsPost.modification_date = new Date();
        this.newsPostService.updateNewsPost(this.newsPost).subscribe({
          next: (newsPost) => this.onSuccess(newsPost),
          error: (err) => this.onError(err)
        });
      }
    }
  }

  /** Event handler to handle cancelling the editor and going back to
   * the previous organization page.
   * @returns {void}
   */
  onCancel(): void {
    this.router.navigate([`news`]);
  }

  /** Event handler to handle the first change in the organization name field
   * Automatically generates a slug from the organization name (that can be edited)
   * @returns {void}
   */
  generateSlug(): void {
    const author = this.newsPostForm.controls['author'].value;
    const slug = this.newsPostForm.controls['slug'].value;
    if (author && !slug) {
      var generatedSlug = author.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
      this.newsPostForm.setControl('slug', new FormControl(generatedSlug));
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess(newsPost: NewsPost): void {
    this.router.navigate(['/news/', newsPost.slug]);

    let message: string =
      this.newsPost_slug === 'new' ? 'Post Created' : 'Post Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.newsPost_slug === 'new'
        ? 'Error: Post Not Created'
        : 'Error: Post Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }
}
