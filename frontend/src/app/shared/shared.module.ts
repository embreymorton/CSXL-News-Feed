import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Angular Material Modules */
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { MatCheckboxModule } from '@angular/material/checkbox';

/* UI Widgets */
import { SocialMediaIcon } from '../shared/social-media-icon/social-media-icon.widget';
import { SearchBar } from './search-bar/search-bar.widget';
import { EventCard } from './event-card/event-card.widget';
import { RouterModule } from '@angular/router';
import { EventList } from './event-list/event-list.widget';
import { UserLookup } from './user-lookup/user-lookup.widget';
import { CommunityAgreement } from './community-agreement/community-agreement.widget';
import { SlackInviteBox } from './slack-invite-box/slack-invite-box.widget';

import { UserChipList } from './user-chip-list/user-chip-list.widget';
import { ProfileAboutCard } from './profile-about-card/profile-about-card.widget';

@NgModule({
  declarations: [
    SocialMediaIcon,
    SearchBar,
    EventCard,
    EventList,
    UserLookup,
    UserChipList,
    SlackInviteBox,
    CommunityAgreement,
    ProfileAboutCard
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatChipsModule,
    MatTableModule,
    MatCardModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    MatCheckboxModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule,
    RouterModule
  ],
  exports: [
    SocialMediaIcon,
    SearchBar,
    EventCard,
    EventList,
    UserLookup,
    UserChipList,
    ProfileAboutCard
  ]
})
export class SharedModule {}
