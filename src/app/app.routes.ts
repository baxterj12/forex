import { Routes } from '@angular/router';
import { HomeComponent } from './home/app.home';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  // Add other routes as needed
];
