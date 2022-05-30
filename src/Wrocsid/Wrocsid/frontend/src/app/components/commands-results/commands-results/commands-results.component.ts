import { Component, Input, OnInit } from '@angular/core';
import { Target } from 'src/app/Model';

@Component({
  selector: 'app-commands-results',
  templateUrl: './commands-results.component.html',
  styleUrls: ['./commands-results.component.css']
})
export class CommandsResultsComponent implements OnInit {

  @Input() target!: Target
  
  constructor() { }

  ngOnInit(): void {
  }

}
