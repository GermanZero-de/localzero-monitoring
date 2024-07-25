import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import  NavigationTile  from '@/app/components/NavigationTile';

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories#default-export
const meta = {
  title: 'monitor/NavigationTile',
  component: NavigationTile,
  parameters: {
    // Optional parameter to center the component in the Canvas. More info: https://storybook.js.org/docs/configure/story-layout
    layout: 'centered',
  },
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
  tags: ['autodocs'],
  // More on argTypes: https://storybook.js.org/docs/api/argtypes
  argTypes: {
    children: {
      control: 'text',
    },
  },
  // Use `fn` to spy on the onClick arg, which will appear in the actions panel once invoked: https://storybook.js.org/docs/essentials/actions#action-args
  args: {},
} satisfies Meta<typeof NavigationTile>;

export default meta;
type Story = StoryObj<typeof meta>;

// More on writing stories with args: https://storybook.js.org/docs/writing-stories/args
export const CardBig: Story = {
  args: {
    isBigCard: true,
    title: 'Big Card example',
    subtitle:"test",
    children: <div>This is custom slot content</div>
  },
};

export const CardSmall: Story = {
  args: {
    isBigCard: false,
    title: 'Small Card example',
    subtitle:"test",
    children: <div>This is custom slot content</div>
  },
};

/*
export const MultipleCards: Story = {
  render: () => {
    const cardsData = [
      { title: 'Card 1', subtitle: 'Topic 1', children: <div>Content for Card 1</div> },
      {  title: 'Card 2', subtitle: 'Topic 2', children: <div>Content for Card 2</div> },
      {  title: 'Card 3', subtitle: 'Topic 3', children: <div>Content for Card 3</div> },
    ];

    return (
      <div style={{ display: 'flex', gap: '1rem' }}>
        {cardsData.map((card, index) => (
          <NavigationTile key={index} {...card} />
        ))}
      </div>
    );
  },
};*/