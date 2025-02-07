import { Component, OnInit } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { ApiService } from './../apiconnect/app.apiconnect';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormControl, FormsModule } from '@angular/forms'; // Import FormsModule

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ HttpClientModule, CommonModule, FormsModule],
  providers: [ApiService ],
  templateUrl: './app.home.html',
  styleUrl: './app.home.css'
})
export class HomeComponent implements OnInit {

  // Title of the home component
  title = "Home"
  // Object to hold currency balances
  balances: { [key: string]: number } = {};
  // Object to hold currency exchange rates
  rates: { [key: string]: number } = {};
  // Current date and time string
  currentDate: string ='';
  // Fees percentage
  fees: number = 5;
  // State of the button
  buttonState: boolean = false;
  // Object to hold rates with fees applied
  ratesWithFees: Object = {}
  // Type of the first value in rates
  type: string = "";
  // Currency to view, default is USD
  viewedCurrency: string = "USD"; // Private variable for viewedCurrency

  // FormControl for viewedCurrency
  viewedCurrencyControl = new FormControl(this.viewedCurrency);

  // Constructor to inject ApiService
  constructor(private apiService: ApiService) {}
  // OnInit lifecycle hook
  ngOnInit(): void {
    // Fetch balances, rates, current date, fees, and rates with fees on component initialization
    this.getBalances();
    setTimeout(() => this.getRates(), 100); 
    setTimeout(() => this.updateCurrentDate(), 100);
    setTimeout(() => this.getFees(), 100);
    setTimeout(() => this.getRatesWithFees(), 200);
    setTimeout(() => this.getType(), 100);
  }

  // Method to fetch balances from the API
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

  // Method to determine the type of the first value in rates
  getType(): void {
      const firstValue = Object.values(this.rates)[0];
      this.type = typeof firstValue;
  }

  // Method to get the type of a given value
  getTypeOf(value: any): string {
    return typeof value
  }

  // Method to fetch exchange rates for a given country
  getRates(country: string = this.viewedCurrency): void {
    this.apiService.getRates(country).subscribe(
      (rate_data) => {
        console.log('New rates:', rate_data);
        this.rates = Object.fromEntries(
          Object.entries(rate_data).map(([key, value]) => [key, +value])
        );
        this.getRatesWithFees();
      },
      (error) => {
        console.error('Error fetching rates:', error)
      }
    );
  }

  // Method to fetch new exchange rates and apply fees
  getNewRates(country: any): void {
    this.getRates(country);
    setTimeout(() => this.getRatesWithFees(), 100);
  }

  // Method to apply fees to exchange rates
  getRatesWithFees(): void {
    let withFees = Object.fromEntries(
      Object.entries(this.rates).map(([key, value]) => [key, value * (1 - (this.fees/100))])
    );
    this.ratesWithFees = withFees;
  }

  // Method to make a trade
  makeTrades(from: string, to: string, amount: number, fees: number): void {
    this.apiService.makeTrade(from, to, amount, fees).subscribe(
      (response) => {
        console.log('Trade successful:', response);
      },
      (error) => {
        console.error('Error making trade:', error);
      }
    );
    this.getBalances();
  }

  // Method to update the current date and time
  updateCurrentDate(): void {
    const now = new Date();
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', hour: '2-digit', minute: '2-digit' };
    this.currentDate = now.toLocaleString('en-US', options);
  }

  // Method to determine fees based on the current date and time
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

  // Method to toggle the button state
  toggleButton(): void {
    this.buttonState = !this.buttonState;
  }

}

