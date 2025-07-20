import User from './User';

class Admin extends User {
    role: string = 'admin';
    groupId: number;
    constructor(displayName: string, universityId: number, userId: number, groupId: number) {
        super(displayName, universityId, userId);
        this.groupId = groupId;
    }
}
export default Admin;
