import { Component, OnInit, inject } from '@angular/core';
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
import { NewsPost } from '../news-post.model';
import { NewsPostService } from '../news-post.service';
import { Profile } from 'src/app/profile/profile.service';
import { NewsPostDetailResolver } from '../news.resolver';
import { Observable, map } from 'rxjs';

@Component({
  selector: 'app-news-post-editor',
  templateUrl: './news-post-editor.component.html',
  styleUrls: ['./news-post-editor.component.css']
})
export class NewsPostEditorComponent implements OnInit {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: 'news/:slug/edit',
    component: NewsPostEditorComponent,
    title: 'News Post Editor',
    resolve: {
      profile: profileResolver,
      newsPost: NewsPostDetailResolver
    }
  };

  public drafts: NewsPost[] = [];

  /** Store the organization.  */
  public newsPost: NewsPost;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  /** Store the organization id. */
  newsPost_slug: string = 'new';

  public adminPermission$: Observable<boolean>;

  isAdmin: boolean = false;

  /** Add validators to the form */
  author = new FormControl('');
  slug = new FormControl('', [
    Validators.required,
    Validators.pattern('^(?!new$)[a-z0-9-]+$')
  ]);
  image_url = new FormControl('');
  headline = new FormControl('', [
    Validators.required,
    Validators.maxLength(15000)
  ]);
  synopsis = new FormControl('', [
    Validators.required,
    Validators.maxLength(15000)
  ]);
  main_story = new FormControl('', [Validators.maxLength(200000000000)]);

  organization_id = new FormControl('', [
    Validators.pattern('^[0-9]*$'),
    Validators.maxLength(2)
  ]);

  /** Organization Editor Form */
  public newsPostForm = this.formBuilder.group({
    headline: this.headline,
    synopsis: this.synopsis,
    main_story: this.main_story,
    organization_id: this.organization_id,
    slug: this.slug,
    image_url: this.image_url
  });
  fullWidth: any;

  /** Constructs the organization editor component */
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private newsPostService: NewsPostService,
    protected permission: PermissionService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      newsPost: NewsPost;
    };
    this.profile = data.profile;
    this.newsPost = data.newsPost;
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');

    /** Get id from the url */
    let newsPost_slug = this.route.snapshot.params['slug'];
    this.newsPost_slug = newsPost_slug;

    if (newsPost_slug != 'new') {
      /** Set organization form data */
      this.newsPostForm.setValue({
        headline: this.newsPost.headline,
        synopsis: this.newsPost.synopsis,
        main_story: this.newsPost.main_story,
        organization_id: this.newsPost.organization_id
          ? String(this.newsPost.organization_id)
          : '',
        slug: this.newsPost.slug,
        image_url: this.newsPost.image_url
      });
    }
  }

  ngOnInit() {
    if (this.profile != null && this.profile.id != null) {
      this.newsPostService
        .getDraftsByAuthor(this.profile.id)
        .subscribe((value) => {
          this.drafts = value;
        });
    }
    this.adminPermission$.subscribe((value) => (this.isAdmin = value));
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.newsPostForm.valid) {
      Object.assign(this.newsPost, this.newsPostForm.value);

      if (this.newsPost.state != 'published') this.newsPost.state = 'incoming';

      if (
        this.newsPostForm.value.organization_id == '' ||
        Number(this.newsPostForm.value.organization_id) > 17
      ) {
        this.newsPost.organization_id = null;
      }

      if (this.newsPostForm.value.image_url == '') {
        this.newsPost.image_url = null;
      }

      if (this.newsPost_slug == 'new') {
        this.newsPost.id = null;
        this.newsPost.time = new Date();
        this.newsPost.modification_date = new Date();

        if (this.profile != null) {
          this.newsPost.author_id = this.profile.id;
        } else {
          this.newsPost.author_id = null;
        }
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

  onSubmitDraft(): void {
    if (this.newsPostForm.valid) {
      Object.assign(this.newsPost, this.newsPostForm.value);
      if (this.newsPost.state != 'published' || this.isAdmin) {
        this.newsPost.state = 'draft';
      }
      if (
        this.newsPostForm.value.organization_id == '' ||
        Number(this.newsPostForm.value.organization_id) > 17
      ) {
        this.newsPost.organization_id = null;
      }

      if (this.newsPost_slug == 'new') {
        this.newsPost.id = null;
        this.newsPost.time = new Date();
        this.newsPost.modification_date = new Date();

        if (this.profile != null) {
          this.newsPost.author_id = this.profile.id;
        } else {
          this.newsPost.author_id = null;
        }

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
    const headline = this.newsPostForm.controls['headline'].value;
    const slug = this.newsPostForm.controls['slug'].value;
    if (headline && !slug) {
      var generatedSlug = headline.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
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

  public editable(): boolean {
    if (
      this.newsPost_slug === 'new' ||
      this.newsPost.author_id === this.profile!.id
    ) {
      return true;
    }

    if (this.newsPost.author_id !== this.profile!.id) {
      return this.isAdmin;
    } else {
      return false;
    }
  }
}
