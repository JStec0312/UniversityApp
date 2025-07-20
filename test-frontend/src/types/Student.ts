import User from './User';
class Student extends User {
    role: string = 'student';
    constructor(displayName: string, university_id: number, user_id: number) {
        super(displayName, university_id, user_id);
    }
}
export default Student;
