import { Component, Input } from '@angular/core';
import { NewsPost } from '../../news-post.model';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'news-full-card',
  templateUrl: './news-full-card.component.html',
  styleUrls: ['./news-full-card.component.css']
})
export class NewsFullCardComponent {
  @Input() post!: NewsPost;
  @Input() profile!: Profile;

  constructor() {}

  get paragraphs() {
    return this.post.main_story.split('\n');
  }
}
