import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WishlistHomeComponent } from './home/Wishlist-home.component';
import { WishlistNewComponent } from './new/Wishlist-new.component';
import { WishlistDetailComponent } from './detail/Wishlist-detail.component';

const routes: Routes = [
  {path: '', component: WishlistHomeComponent},
  { path: 'new', component: WishlistNewComponent },
  { path: ':id', component: WishlistDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Wishlist-detail-permissions'
      }
    }
  }
];

export const WISHLIST_MODULE_DECLARATIONS = [
    WishlistHomeComponent,
    WishlistNewComponent,
    WishlistDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WishlistRoutingModule { }