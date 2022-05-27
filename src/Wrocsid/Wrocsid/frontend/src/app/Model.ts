export class Target {
    identifier: string
    channel_id: string
    metadata: {
        ip: string
        country: string
        city: string
        os: string
    }
    online: Boolean

    constructor(target?: Target) {
        this.identifier = target?.identifier ?? '',
        this.channel_id = target?.channel_id ?? '',
        this.metadata = target?.metadata ?? {
            ip: '',
            country: '',
            city: '',
            os: '',
        },
        this.online = target?.online ?? true
    }
}