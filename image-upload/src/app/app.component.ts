import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [HttpClientModule, CommonModule]
})
export class AppComponent {
  title = 'PNG Checker';
  selectedFile: File | null = null;
  imageSpecs: any = null;
  errorMessage: string | null = null;

  constructor(private http: HttpClient) { }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  onUpload(): void {
    if (this.selectedFile) {
      const formData: FormData = new FormData();
      formData.append('file', this.selectedFile, this.selectedFile.name);

      this.http.post('http://127.0.0.1:5000/api/upload', formData)
        .subscribe({
          next: (response: any) => {
            this.imageSpecs = response;
            this.errorMessage = null;
          },
          error: (error) => {
            this.errorMessage = error.error.error;
            this.imageSpecs = null;
          }
        });
    }
  }
}