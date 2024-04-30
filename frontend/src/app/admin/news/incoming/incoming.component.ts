import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { NewsPost } from 'src/app/news/news-post.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminNewsService } from '../admin-news.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-admin-incoming-post',
  templateUrl: './admin-incoming-post.component.html',
  styleUrls: ['./admin-incoming-post.component.css']
})
export class AdminIncomingPostComponent {
  public incomingPosts$: Observable<NewsPost[]>;

  public displayedColumns: string[] = ['headline'];

  /** Route information to be used in Admin Routing Module */
  public static Route = {
    path: 'news/incoming',
    component: AdminIncomingPostComponent,
    title: 'News Administration',
    canActivate: [permissionGuard('newsPost.incoming', 'newsPost')]
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private adminNewsService: AdminNewsService
  ) {
    this.incomingPosts$ = adminNewsService.newPosts$;
    adminNewsService.list_incoming();
  }

  /** Event handler to open the NewsPost Editor to create a new NewsPost */
  createNewsPost(): void {
    // Navigate to the org editor for a new NewsPost (slug = create)
    this.router.navigate(['news', 'new', 'edit']);
  }

  /** Event handler to navigate to the main sotry of a NewsPost when clicked */
  navigateToPageDetail(element: NewsPost): void {
    this.router.navigate(['news', element.slug]);
  }

  /** Delete a NewsPost object from the backend database table using the backend HTTP post request.
   * @param newsPost_id: unique number representing the updated organization
   * @returns void
   */
  deleteNewsPost(newsPost: NewsPost): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this News Post?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.adminNewsService.deleteNewsPost(newsPost).subscribe(() => {
        this.snackBar.open('This News Post has been deleted.', '', {
          duration: 2000
        });
      });
    });
  }

  /** Event handler to open the NewsPost Editor to update a NewsPost */
  updateNewsPost(newsPost: NewsPost): void {
    // Navigate to the org editor for a new NewsPost (slug = create)
    this.router.navigate(['news', newsPost.slug, 'edit']);
  }

  publishNewsPost(newsPost: NewsPost): void {
    let confirmPublish = this.snackBar.open(
      'Are you sure you want to publish this News Post?',
      'Publish',
      { duration: 15000 }
    );
    confirmPublish.onAction().subscribe(() => {
      this.adminNewsService.publishNewsPost(newsPost).subscribe(() => {
        this.snackBar.open('This News Post has been Published.', '', {
          duration: 2000
        });
      });
    });
  }

  archiveNewsPost(newsPost: NewsPost): void {
    let confirmPublish = this.snackBar.open(
      'Are you sure you want to archive this News Post?',
      'Archive',
      { duration: 15000 }
    );
    confirmPublish.onAction().subscribe(() => {
      this.adminNewsService.archiveNewsPost(newsPost).subscribe(() => {
        this.snackBar.open('This News Post has been Archived.', '', {
          duration: 2000
        });
      });
    });
  }
}
