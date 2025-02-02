import { Component, OnInit } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { ApiService } from './../apiconnect/app.apiconnect';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ HttpClientModule, CommonModule],
  providers: [ApiService ],
  templateUrl: './app.home.html',
  styleUrl: './app.home.css'
})
export class HomeComponent implements OnInit {

  title = "Home"
  balances: { [key: string]: number } = {};
  rates: { [key: string]: number } = {};
  currentDate: string ='';
  fees: number = 5;
  buttonState: boolean = false;
  ratesWithFees: Object = {}
  type: string = "";


  constructor(private apiService: ApiService) {}
  ngOnInit(): void {
    this.getBalances();
    setTimeout(() => this.getRates(), 100); 
    setTimeout(() => this.updateCurrentDate(), 100);
    setTimeout(() => this.getFees(), 100);
    setTimeout(() => this.getRatesWithFees(), 100);
    setTimeout(() => this.getType(), 100);
  }

  getBalances(): void {
    this.apiService.getAllBalances().subscribe(
      (data) => {
        // Assuming the data is in a key-value pair format
        this.balances = Object.fromEntries(
          Object.entries(data).map(([key, value]) => [key, +value])
        );
      },
      (error) => {
        console.error('Error fetching balances:', error);
      }
    );
  }

  getType(): void {
      const firstValue = Object.values(this.rates)[0];
      this.type = typeof firstValue;
  }

  getRates(): void {
    this.apiService.getRates().subscribe(
      (rate_data) => {
        this.rates = Object.fromEntries(
          Object.entries(rate_data).map(([key, value]) => [key, Number(value)])
        );
      },
      (error) => {
        console.error('Error fetching rates:', error)
      }
    );
  }

  getRatesWithFees(): void {
    let withFees = Object.fromEntries(
      Object.entries(this.rates).map(([key, value]) => [key, value * (1 - (this.fees/100))])
    );
    this.ratesWithFees = withFees;
  }

  updateCurrentDate(): void {
    const now = new Date();
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', hour: '2-digit', minute: '2-digit' };
    this.currentDate = now.toLocaleString('en-US', options);
  }

  getFees(): void {
    const day = this.currentDate.split(' ')[0];  // Get the day name
    const time = this.currentDate.split(' ')[1].trim();  // Get the time
    if ((day === "Friday" && time >= "5:00 PM") || 
        (day === "Saturday") || 
        (day === "Sunday" && time <= "6:00 PM")) {
      this.fees = 0.5;
    } 
    else {
      this.fees = 0;
    }
  }

  toggleButton(): void {
    this.buttonState = !this.buttonState;
  }

}

