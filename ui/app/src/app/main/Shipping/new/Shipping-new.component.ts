import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Shipping-new',
  templateUrl: './Shipping-new.component.html',
  styleUrls: ['./Shipping-new.component.scss']
})
export class ShippingNewComponent {
  @ViewChild("ShippingForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}