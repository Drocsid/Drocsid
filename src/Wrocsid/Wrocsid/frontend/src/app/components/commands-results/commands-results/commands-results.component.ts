import { Component, Input, OnInit } from '@angular/core';
import { firstValueFrom, interval } from 'rxjs';
import { Target } from 'src/app/Model';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';

@Component({
  selector: 'app-commands-results',
  templateUrl: './commands-results.component.html',
  styleUrls: ['./commands-results.component.css']
})
export class CommandsResultsComponent implements OnInit {

  @Input() target$!: Target

  target_results$!: any
  loading_bar_finished: boolean = false
  
  constructor(private wrocsid: WrocsidService) { }

  ngOnInit(): void {
    this.wrocsid.getTargetResults(this.target$.identifier).subscribe((data) => {
      this.target_results$ = data
    })

    interval(10 * 1000).subscribe(() => {
      this.wrocsid.getTargetResults(this.target$.identifier).subscribe(data => {
        if (data) {
          this.changeLoadingStatus()
          this.target_results$ = data
          console.log(data)
        }
      })
    })
  }

  changeLoadingStatus() {
    this.loading_bar_finished = !this.loading_bar_finished
  }

  isPicture(content_type: string) {
    return content_type === "image/jpeg" 
  }

  isAudio(content_type: string) {
    return content_type === "audio/x-wav"
  }
}