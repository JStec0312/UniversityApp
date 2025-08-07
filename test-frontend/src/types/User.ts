class User{
    displayName: string;
    universityId: number;
    userId: number;
    avatarUrl?: string;
    constructor(displayName: string, universityId: number, userId: number, avatarUrl?: string) {
        this.displayName = displayName;
        this.universityId = universityId;
        this.userId = userId;
        this.avatarUrl = avatarUrl;
    }

}
export default User;
