import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { NewsPost } from 'src/app/news/news-post.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AdminNewsService } from '../admin-news.service';
import { Observable, finalize } from 'rxjs';
import { PageEvent } from '@angular/material/paginator';
import { Paginated } from 'src/app/pagination';

@Component({
  selector: 'app-admin-news-list',
  templateUrl: './admin-news-list.component.html',
  styleUrls: ['./admin-news-list.component.css']
})
export class AdminNewsListComponent {
  public page: Paginated<NewsPost>;

  public displayedColumns: string[] = ['headline'];

  private static PaginationParams = {
    page: 0,
    page_size: 15,
    order_by: 'headline',
    filter: ''
  };

  /** Route information to be used in Admin Routing Module */
  public static Route = {
    path: 'news',
    component: AdminNewsListComponent,
    title: 'News Administration',
    canActivate: [permissionGuard('newsPost.list', 'newsPost')],
    resolve: {
      page: () =>
        inject(AdminNewsService).list(AdminNewsListComponent.PaginationParams)
    }
  };

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private adminNewsService: AdminNewsService,
    route: ActivatedRoute
  ) {
    let data = route.snapshot.data as { page: Paginated<NewsPost> };
    this.page = data.page;
    this.page.params = AdminNewsListComponent.PaginationParams;
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
      this.adminNewsService
        .deleteNewsPost(newsPost)
        .pipe(finalize(() => this.refreshPage()))
        .subscribe(() => {
          this.snackBar.open('This News Post has been Deleted.', '', {
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

  archiveNewsPost(newsPost: NewsPost): void {
    let confirmArchive = this.snackBar.open(
      'Are you sure you want to archive this News Post?',
      'Archive',
      { duration: 15000 }
    );
    confirmArchive.onAction().subscribe(() => {
      this.adminNewsService
        .archiveNewsPost(newsPost)
        .pipe(finalize(() => this.refreshPage()))
        .subscribe(() => {
          this.snackBar.open('This News Post has been Archived.', '', {
            duration: 2000
          });
        });
    });
  }

  handlePageEvent(e: PageEvent) {
    let paginationParams = this.page.params;
    paginationParams.page = e.pageIndex;
    paginationParams.page_size = e.pageSize;
    this.adminNewsService
      .list(paginationParams)
      .subscribe((page) => (this.page = page));
  }

  refreshPage() {
    this.adminNewsService
      .list(AdminNewsListComponent.PaginationParams)
      .subscribe((page) => (this.page = page));
  }
}
