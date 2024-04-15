/**
 * The NewsPost Model defines the shape of NewsPost data
 * retrieved from the News Post Service and the API.
 *
 * @author Embrey Morton, Ishmael Percy, "Jayson Mbugua", "Alphonzo Dixon"
 * @copyright 2024
 * @license MIT
 */

/** Interface for Organization Type (used on frontend for organization detail) */
export interface NewsPost {
  id: number;
  headline: string;
  synopsis: string;
  main_story: string;
  author: string;
  organization: string;
  state: string;
  slug: string;
  image_url: string;
  publish_date: string;
  modification_date: string;
}
