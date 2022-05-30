import { Component, Input, OnInit } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { Target } from 'src/app/Model';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';

@Component({
  selector: 'app-commands-results',
  templateUrl: './commands-results.component.html',
  styleUrls: ['./commands-results.component.css']
})
export class CommandsResultsComponent implements OnInit {

  @Input() target!: Target

  target_results!:any
  loading_bar_finished: boolean = false
  
  constructor(private wrocsid: WrocsidService) { }

  async ngOnInit(): Promise<void> {
    this.target_results = await firstValueFrom(this.wrocsid.getTargetResults(this.target.identifier))

    let temp_results
    while(true) {
      this.changeLoadingStatus()
      await this.delay(10 * 1000)
      temp_results = await firstValueFrom(this.wrocsid.getTargetResults(this.target.identifier))
      this.changeLoadingStatus()
      if(!temp_results) {
        continue
      }
      this.target_results = temp_results
    }
  }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

  changeLoadingStatus() {
    this.loading_bar_finished = !this.loading_bar_finished
  }
}