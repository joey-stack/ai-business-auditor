import React from "react";
import { Composition } from "remotion";
import { TikTokVideo1 } from "./TikTokVideo1";
import { TikTokVideo2 } from "./TikTokVideo2";
import { TikTokVideo3 } from "./TikTokVideo3";

export const RemotionComposition: React.FC = () => {
  return (
    <>
      <Composition
        id="TikTokVideo1"
        component={TikTokVideo1}
        durationInFrames={1465}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TikTokVideo2"
        component={TikTokVideo2}
        durationInFrames={1520}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TikTokVideo3"
        component={TikTokVideo3}
        durationInFrames={1925}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};

