import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import { AdminRoleDetailsComponent } from './roles/details/admin-role-details.component';
import { AdminRolesListComponent } from './roles/list/admin-roles-list.component';
import { AdminUsersListComponent } from './users/list/admin-users-list.component';
import { AdminNewsListComponent } from './news/list/admin-news-list.component';
import { AdminIncomingPostComponent } from './news/incoming/incoming.component';
import { AdminArchivedPostsComponent } from './news/archived/admin-archived-posts.component';

const routes: Routes = [
  {
    path: '',
    component: AdminComponent,
    children: [
      AdminUsersListComponent.Route,
      AdminRolesListComponent.Route,
      AdminRoleDetailsComponent.Route,
      AdminNewsListComponent.Route,
      AdminIncomingPostComponent.Route,
      AdminArchivedPostsComponent.Route
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule {}
