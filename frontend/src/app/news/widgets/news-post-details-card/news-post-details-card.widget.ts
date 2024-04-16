import { Component, Input, OnDestroy, OnInit } from '@angular/core';

import { NewsPost } from '../../news-post/news-post.model';
import { Profile } from 'src/app/models.module';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NewsPostService } from '../../news-post.service';
import { PermissionService } from 'src/app/permission.service';
import { Router } from '@angular/router';

@Component({
  selector: 'news-post-details-card',
  templateUrl: './news-post-details-card.widget.html',
  styleUrls: ['./news-post-details-card.widget.css']
})
export class NewsPostDetailsCard {
  @Input() post!: NewsPost;

  @Input() profile!: Profile;

  constructor(
    public snackBar: MatSnackBar,
    protected newsService: NewsPostService,
    private permission: PermissionService,
    private router: Router
  ) {}

  deletePost(post: NewsPost): void {
    let confirmDelete = this.snackBar.open(
      'Are you sure you want to delete this post?',
      'Delete',
      { duration: 15000 }
    );
    confirmDelete.onAction().subscribe(() => {
      this.newsService.deleteNewsPost(post).subscribe(() => {
        this.snackBar.open('Event Deleted', '', { duration: 2000 });
        this.router.navigateByUrl('/news');
      });
    });
  }

  onShareButtonClick() {
    // Write the URL to the clipboard
    navigator.clipboard.writeText(
      'https://' + window.location.host + '/news/' + this.post.slug
    );
    // Open a snackbar to alert the user
    this.snackBar.open('Event link copied to clipboard.', '', {
      duration: 3000
    });
  }
}
