// Original file keeps default export
import Post from '../models/post';

export default class PostService {
    getPost(id: string): Post {
        return { id, title: 'Hello', content: 'World' };
    }
}