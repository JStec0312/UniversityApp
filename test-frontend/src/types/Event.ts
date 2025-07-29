export class Event {
  description: string;
  end_date: string;
  id?: number;
  image_url?: string;
  location: string;
  start_date: string;
  title: string;
  group_name: string;

  constructor(description: string, end_date: string, start_date: string, title: string,  id?: number, image_url?: string, location?: string, group_name?: string) {
    this.description = description;
    this.end_date = end_date;
    this.start_date = start_date;
    this.title = title;
    this.group_name = group_name ;
    this.id = id;
    this.image_url = image_url;
    this.location = location || "";
  }
}
