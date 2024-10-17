import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Shipping-card.component.html',
  styleUrls: ['./Shipping-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Shipping-card]': 'true'
  }
})

export class ShippingCardComponent {


}