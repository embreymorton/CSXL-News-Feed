/**
 * The NewsPost Model defines the shape of NewsPost data
 * retrieved from the News Post Service and the API.
 *
 * @author Embrey Morton, Ishmael Percy, "Jayson Mbugua", "Alphonzo Dixon"
 * @copyright 2024
 * @license MIT
 */

import { Organization } from 'src/app/organization/organization.model';
import { Profile } from '../models.module';

/** Interface for Organization Type (used on frontend for organization detail) */
export interface NewsPost {
  id: number | null;
  headline: string;
  synopsis: string;
  main_story: string;
  author_id: number | null;
  author: Profile | null;
  organization_id: number | null;
  organization: Organization | null;
  state: string;
  slug: string;
  image_url: string | null;
  time: Date;
  modification_date: Date;
}

export interface NewsPostJson {
  id: number | null;
  headline: string;
  synopsis: string;
  main_story: string;
  author_id: number | null;
  author: Profile | null;
  organization_id: number | null;
  organization: Organization | null;
  state: string;
  slug: string;
  image_url: string;
  time: Date;
  modification_date: Date;
}

export const parsePostJson = (postJson: NewsPostJson): NewsPost => {
  return Object.assign({}, postJson, { time: new Date(postJson.time) });
};
