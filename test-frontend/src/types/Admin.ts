import User from './User';

class Admin extends User {
    role: string = 'admin';
    groupId: number;
    groupName: string;
    constructor(displayName: string, universityId: number, userId: number, groupId: number, groupName: string) {
        super(displayName, universityId, userId);
        this.groupId = groupId;
        this.groupName = groupName;
    }
}
export default Admin;
