import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
    private apiUrl = "http://127.0.0.1:5001" //python local

    constructor(private http: HttpClient) {}

    //TRADE DATA
    getTrades() {
        return this.http.get(`${this.apiUrl}/trades`);
    }

    getRates(country: string = 'USD') { // Observable<any> {, country: string = 'USD' is param
        return this.http.get(`${this.apiUrl}/get_exrates?country=${country}`);
    }

    getAllBalances() {
        return this.http.get(`${this.apiUrl}/getAllBalances`)
    }

    makeTrade(from: string, to: string, amount: number, fees: number) {
        return this.http.get(`${this.apiUrl}/makeTrade?from=${from}&to=${to}&amount=${amount}&fee=${fees}`)
    }
}