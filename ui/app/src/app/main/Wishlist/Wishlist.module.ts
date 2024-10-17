import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WISHLIST_MODULE_DECLARATIONS, WishlistRoutingModule} from  './Wishlist-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WishlistRoutingModule
  ],
  declarations: WISHLIST_MODULE_DECLARATIONS,
  exports: WISHLIST_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WishlistModule { }