import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppTitleStrategy } from './app-title.strategy';
import { GateComponent } from './gate/gate.component';
import { HomeComponent } from './home/home.component';
import { ProfileEditorComponent } from './profile/profile-editor/profile-editor.component';
import { AboutComponent } from './about/about.component';
import { NewsFeedComponent } from './news/news-feed/news-feed.component';
import { NewsPostEditorComponent } from './news/news-post-editor/news-post-editor.component';
import { NewsPostComponent } from './news/news-post/news-post.component';

const routes: Routes = [
  HomeComponent.Route,
  AboutComponent.Route,
  GateComponent.Route,
  NewsPostComponent.Route,
  NewsFeedComponent.Route,
  NewsPostEditorComponent.Route,
  {
    path: 'coworking',
    title: 'Cowork in the XL',
    loadChildren: () =>
      import('./coworking/coworking.module').then((m) => m.CoworkingModule)
  },
  {
    path: 'profile',
    title: 'Profile',
    loadChildren: () =>
      import('./profile/profile.module').then((m) => m.ProfileModule)
  },
  {
    path: 'academics',
    title: 'Academics',
    loadChildren: () =>
      import('./academics/academics.module').then((m) => m.AcademicsModule)
  },
  {
    path: 'admin',
    title: 'Admin',
    loadChildren: () =>
      import('./admin/admin.module').then((m) => m.AdminModule)
  },
  {
    path: 'organizations',
    title: 'CS Organizations',
    loadChildren: () =>
      import('./organization/organization.module').then(
        (m) => m.OrganizationModule
      )
  },
  {
    path: 'events',
    title: 'Experimental',
    loadChildren: () =>
      import('./event/event.module').then((m) => m.EventModule)
  },
  {
    path: 'ta-application',
    title: 'TA Applications',
    loadChildren: () =>
      import('./ta-application/ta-application.module').then(
        (m) => m.ApplicationsModule
      )
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled',
      anchorScrolling: 'enabled'
    })
  ],
  exports: [RouterModule],
  providers: [AppTitleStrategy.Provider]
})
export class AppRoutingModule {}
