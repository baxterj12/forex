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

    getRates() { // Observable<any> {, country: string = 'USD' is aram
        return this.http.get(`${this.apiUrl}/get_exrates`);
    }

    getAllBalances() {
        return this.http.get(`${this.apiUrl}/getAllBalances`)
    }
}