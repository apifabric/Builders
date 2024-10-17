import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ShippingHomeComponent } from './home/Shipping-home.component';
import { ShippingNewComponent } from './new/Shipping-new.component';
import { ShippingDetailComponent } from './detail/Shipping-detail.component';

const routes: Routes = [
  {path: '', component: ShippingHomeComponent},
  { path: 'new', component: ShippingNewComponent },
  { path: ':id', component: ShippingDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Shipping-detail-permissions'
      }
    }
  }
];

export const SHIPPING_MODULE_DECLARATIONS = [
    ShippingHomeComponent,
    ShippingNewComponent,
    ShippingDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ShippingRoutingModule { }