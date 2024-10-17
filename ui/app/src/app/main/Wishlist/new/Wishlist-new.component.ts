import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Wishlist-new',
  templateUrl: './Wishlist-new.component.html',
  styleUrls: ['./Wishlist-new.component.scss']
})
export class WishlistNewComponent {
  @ViewChild("WishlistForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}