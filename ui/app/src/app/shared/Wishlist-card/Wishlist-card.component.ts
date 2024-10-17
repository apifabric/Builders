import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Wishlist-card.component.html',
  styleUrls: ['./Wishlist-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Wishlist-card]': 'true'
  }
})

export class WishlistCardComponent {


}