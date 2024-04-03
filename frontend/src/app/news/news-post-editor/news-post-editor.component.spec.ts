import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsPostEditorComponent } from './news-post-editor.component';

describe('NewsPostEditorComponent', () => {
  let component: NewsPostEditorComponent;
  let fixture: ComponentFixture<NewsPostEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewsPostEditorComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewsPostEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
