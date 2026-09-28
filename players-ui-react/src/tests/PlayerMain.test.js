import { render, screen } from '@testing-library/react';
import PlayerMain from '../components/PlayerMain';

test('renders main header', () => {
  render(<PlayerMain />);
  expect(screen.getByText('Hello Players')).toBeTruthy();
});

test('renders player search fields', () => {
  render(<PlayerMain />);
  expect(screen.getByText(/Player id/i)).toBeTruthy();
  expect(screen.getByText(/Player Country Code/i)).toBeTruthy();
  expect(screen.getAllByRole('button', { name: /Submit/i }).length).toBe(2);
});
