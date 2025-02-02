import { Component, Renderer2, ElementRef } from '@angular/core';
import { RouterOutlet, Router} from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {ApiService} from './../apiconnect/app.apiconnect';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ HttpClientModule, CommonModule, FormsModule],
  providers: [ApiService ],
  templateUrl: './app.login.html',
  styleUrl: './app.login.css'
})
export class LoginComponent {
  title = 'login';
  userInput: string = ''; // To store the input value
  message = "Password not detected"
  constructor(private router: Router) {}

  // Function to update the output
  checkPass(): void {
    console.log(this.userInput); // Optional: Log the input value
    if (this.userInput == "Bax7485") {
      this.message = "Correct Password!"
      this.router.navigate(['/home']);
    }
  }

}